import cv2
import numpy as np
import random

from shapely.geometry import Polygon

from globals.constants import PS_MIN_BLOCK_AREA, COLORS
import helpers.geometry as geometry

class ParkingSpotDetector:
	def __init__(self):
		pass

	def detect(self, image_path, levels = 3):
		image = cv2.imread(image_path)
		
		# Grayscale
		img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
		# Region of interest
		#roi = cv2.selectROI(img)
		#roi = (118, 181, 314, 199)
		
		#image = image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		#img = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

		# Median blur
		blur = cv2.medianBlur(img, 5)
		
		# Otsu's thresolding (thresold, image)
		thresold, thresolded = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

		# Canny Edge Detection
		min_thresold = thresold
		max_thresold = 2 * min_thresold
		edges = cv2.Canny(thresolded, min_thresold, max_thresold)
		
		# Find contours
		(cnts, hierarchy) = cv2.findContours(thresolded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		
		# Draw contours
		#result = image.copy()
		result = np.zeros((img.shape[0], img.shape[1], 3), dtype="uint8")
		#cv2.drawContours(result, cnts, -1, (0,0,255), 2, cv2.LINE_AA)


		approx_ctns = []
		for i, cnt in enumerate(cnts):
			perimeter = cv2.arcLength(cnt, True)
			area = cv2.contourArea(cnt)

			if area > PS_MIN_BLOCK_AREA:
				approx = cv2.approxPolyDP(cnt, 0.005 * perimeter, True)
				approx_ctns.append(approx)
				cv2.drawContours(result, [approx], -1, COLORS[i], 2, cv2.LINE_AA)


		index = [2,3]
		approx_ctns = np.delete(approx_ctns, index)

		simple_ctns = []
		for cnt in approx_ctns:
			cnt = np.asarray(list(map(lambda x: x[0], cnt)))
			simple_ctns.append(geometry.simplify_contour(cnt))

			#for point in geometry.simplify_contour(cnt):
			#	cv2.circle(result, tuple(point), 3, (0,255,0), -1)
		
		
		# Contour sort and group by level (image top and left)
		leveled_cnts = []
		
		for i, cnt in enumerate(simple_ctns):
			levels = 3 if (i == 2 or i == 3) else 2
			points_per_level = int(len(cnt) / levels) # Points per level on parking lines
		
			# Sort points top to bottom and left to right
			lexsorted_index = np.lexsort((cnt[:, 0], cnt[:, 1]))	# Return index sorted 
			points = cnt[lexsorted_index]			# Generate array ofsorted point

			# Interpreting sorted varray elements
			points = points.reshape((levels, points_per_level, 2))    # Reshape x points (two component (x, y)) per level
			
			# Reorder points in groups (left to right)
			for i, p in enumerate(points):
				lexsorted_index = np.lexsort((p[:, 1], p[:, 0]))
				points[i] = points[i, lexsorted_index]

			leveled_cnts.append(points)

		parking_slots = np.array([])

		for k, cnts in enumerate(leveled_cnts):
			for i, cnt in enumerate(cnts):
				for j, point in enumerate(cnt):
					points_per_level = len(cnt) # Points per level on parking lines
					levels = 3 if (k == 2 or k == 3) else 2
					if i < (levels - 1) and j < (points_per_level - 1):
						points = np.append(cnts[i, j:j+2], np.flip(cnts[i+1, j:j+2], axis=0), 0)
						points = np.array([points])

						parking_slots = points if parking_slots.size == 0 else np.append(parking_slots, points, 0)
		
		i = 0
		for ps in parking_slots:
			color = random.uniform(0, 255),random.uniform(0, 255),random.uniform(0, 255)
			for p in ps:
				cv2.circle(result, tuple(p), 3, (0,0,255), -1)
			font = cv2.FONT_HERSHEY_SIMPLEX
			p = geometry.medium_point(ps)
			cv2.putText(result,str(i), tuple(p - 10), font, 0.5,(255,255,255),2,cv2.LINE_AA)
			i += 1
			poly = Polygon(ps)
			#print('---------')
			#print(i)
			#print(poly)
			#print(poly.area)
			real_area = round(poly.area * 0.9555, 2)
			real_length = round(poly.length * 0.9775, 2)
			print(str(real_area).replace('.', ','))

			#cv2.fillPoly(result, np.int_([ps]), color)
		
		alpha = 0.7  # Transparency factor.
		# Following line overlays transparent rectangle over the image
		#result = cv2.addWeighted(result, alpha, image, 1 - alpha, 0)

		# initialize the shape name and approximate the contour
		#shape = "unidentified"
		#peri = cv2.arcLength(c, True)
		#approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		#cv2.imshow("ROI", img)
		#cv2.imshow("Blur", blur)
		#cv2.imshow("Thresold", thresolded)
		#cv2.imshow("Edges", edges)
		cv2.imshow("Result", result)

		cv2.waitKey()

		return parking_slots