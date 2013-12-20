import cv

cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)

def repeat():

	frame = cv.QueryFrame(capture)
	cv.ShowImage("wi", frame)
	cv.WaitKey(10)

while True:
	repeat()
