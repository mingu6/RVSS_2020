import evaluate
from PIL import Image
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt

class PosedImage:
    def __init__(self, json_line):
        img_dict = json.loads(json_line)
        self.pose = np.array(img_dict["pose"])
        self.img_name = img_dict["imgfname"]
        params = cv2.SimpleBlobDetector_Params()
        params.minArea = 4
        # params.minDistBetweenBlobs = 1
        self.blob_detector = cv2.SimpleBlobDetector_create(params)
        self.intrinsics = np.loadtxt('../testData/testCalibration/intrinsic.txt', delimiter=',')

    def write_bearings(self, neuralnet, bearings_file, folder_name=""):
        # Obtain neural net output
        img = Image.open(folder_name+self.img_name)
        heatmap = neuralnet.sliding_window(img)
        #plt.imshow(heatmap)
        #keypoints = self.blob_detector.detect(heatmap)
        #im_with_keypoints = cv2.drawKeypoints(heatmap, keypoints, np.array([]),(0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #cv2.imshow("Keypoints", im_with_keypoints)
        #cv2.waitKey(0)
        # Compute animal bearings here and save to self.animals.
        # Next, you can use all this information to triangulate the animals!
        bearings = {}
        animals = ['crocodile', 'elephant', 'llama', 'snake']
        for i in range(1,5):
            heatmap_cls = np.where(heatmap == i, np.ones_like(heatmap) * 255, np.zeros_like(heatmap))

            heatmap_cls = heatmap_cls.astype(np.uint8)
            keypoints = self.blob_detector.detect(cv2.bitwise_not(heatmap_cls))
            biggest_blob_cls = None
            for kp in keypoints:
                if biggest_blob_cls is None or kp.size > biggest_blob_cls.size:
                    biggest_blob_cls = kp
            if biggest_blob_cls is not None:
                x0 = self.intrinsics[0][2]
                fx = self.intrinsics[0][0]
                diff = x0 - biggest_blob_cls.pt[0] / heatmap.shape[1] * img.width
                bearings[animals[i-1]] = np.arctan(diff / fx)
                #print(animals[i], np.degrees(bearings[animals[i]]))
                #import matplotlib.pyplot as plt
                #plt.imshow(heatmap_cls)
                #plt.scatter(biggest_blob_cls.pt[0], biggest_blob_cls.pt[1])
                #plt.show()

        # For example, finding the llamas:
        # if np.any(heatmap == 2.0):
        #     llama_coords = np.where(heatmap == 2.0)
        #     average_llama = np.mean(llama_coords, axis=1)
        #     bearings["llama"] = ...
        # Now you need to convert this to a horizontal bearing as an angle.
        # Use the camera matrix for this!

        # There are ways to get much better bearings.
        # Try and think of better solutions than just averaging.

        for animal in bearings:
            bearing_dict = {"pose":self.pose.tolist(),
                            "animal":animal,
                            "bearing":bearings[animal]}
            bearing_line = json.dumps(bearing_dict)
            print(bearing_line)
            bearings_file.write(bearing_line + '\n')
            print(">>>>> Image name is: "+self.img_name)
            print(">>>>>>>>>>>>>>>>>>")
            print(bearing_dict)
            print("<<<<<<<<<<<<<<<<<<")
            #plt.show()


if __name__ == "__main__":
    # Set up the network
    exp = evaluate.Evaluate()
    # with open('../system_output/images.txt', 'w') as f:
    #     json.dump({"pose":[0.0 for _ in range(3)],
    #                     "imgfname":'../network/testImages/0.png'}, f)
    # with open('../system_output/images.txt', 'w') as f:
    #     json.dump(list([{"pose":[0.0 for _ in range(6)],
    #                     "imgfname":'../network/testImages/' + str(i) + '.png'} for i in range(10)]), f)
    
    # Read in the images
    num = 1

    images_fname = "../map{}/images.txt".format(num)
    with open(images_fname, 'r') as images_file:
        posed_images = [PosedImage(line) for line in images_file]

    # Compute bearings and write to file
    bearings_fname = "../map{}/bearings.txt".format(num)
    with open(bearings_fname, 'w+') as bearings_file:
        for posed_image in posed_images:
            posed_image.write_bearings(exp, bearings_file, "../map{}/".format(num))
