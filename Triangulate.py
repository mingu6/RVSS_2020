import numpy as np
from slam.SlamMap import SlamMap
import json

def realign_to_frame(f1Tf2, pose):
    angle = pose[2]
    f2Rpose = np.array([[np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]])
    pose_t = pose[:2]
    f2Tpose = to_hom(f2Rpose[:, :, 0], pose_t)

    f1Tpose = f1Tf2 @ f2Tpose
    new_x = f1Tpose[0, 2]
    new_y = f1Tpose[0, 2]
    new_angle = np.arccos(f1Tpose[0, 0])
    return [new_x, new_y, new_angle]
def to_hom(R, t):
    T = np.eye(3)
    T[:2, :2] = R[:, :]
    t = np.asarray(t)
    if len(t.shape) == 2:
        t = t[:, 0]
    T[:2, 2] = t
    return T

def hom_inv(T):
    T_inv = np.eye(3)
    T_inv[:2, :2] = T[:2, :2].T
    T_inv[:2, 2] = -T[:2, :2].T @ T[:2, 2]
    return T_inv
def triangulate_animal(data):

    def rotxyt(theta):
        return np.array([[np.cos(theta), -np.sin(theta)],
                         [np.sin(theta), np.cos(theta)]]).transpose()

    def pline(alpha):
        return np.array([-np.sin(alpha),
                         np.cos(alpha)]).transpose()

    def plinexy(x, y, alpha):
        return np.array([[-np.sin(alpha)],
                         [np.cos(alpha)]]).transpose()

    A = np.zeros((data.shape[0], 2))
    B = np.zeros((data.shape[0], 1))

    for idx in range(data.shape[0]):

        A[idx, :] = pline(data[idx, 3]) @ rotxyt(data[idx, 2])

        B[idx, :] = (pline(data[idx, 3]) @ rotxyt(data[idx, 2])) @ np.array([data[idx, 0], data[idx, 1]])

    #return A, B
    # psuedo inverse
    L = (np.linalg.inv(A.T @ A) @ A.T @ B).T[0]

    return L

if __name__ == '__main__':
    map1f = 'map1/slam.txt'
    map2f = 'map2/slam.txt'
    map3f = 'map3/slam.txt'
    
    bearings1f = 'map1/bearings.txt'
    bearings2f = 'map2/bearings.txt'
    #bearings3f = 'map3/bearings.txt'
    
    slam1 = SlamMap()
    #slam2 = SlamMap()
    #slam3 = SlamMap()
    
    slam1.load(map1f)
    #slam2.load(map2f)
    #slam3.load(map3f)

    #_, f1Rf2, f1tf2 = slam1.compute_tf(slam2)
    #_, f1Rf3, f1tf3 = slam1.compute_tf(slam3)

    #f1Tf2 = to_hom(f1Rf2, f1tf2)
    
    #f1Tf3 = to_hom(f1Rf3, f1tf3)
    

    all_bearings = []

    with open(bearings1f, 'r') as bfile:
        for l in bfile.readlines():
            d = json.loads(l)
            all_bearings.append(d)
    # with open(bearings2f, 'r') as bfile:
    #     for l in bfile.readlines():
    #         d = json.loads(l)
    #         d['pose'] = realign_to_frame(f1Tf2, d['pose'])
    #         all_bearings.append(d)
    # with open(bearings3f, 'r') as bfile:
    #     for l in bfile.readlines():
    #         d = json.loads(l)
    #         d['pose'] = realign_to_frame(f1Tf3, d['pose'])
    #         all_bearings.append(d)
    animals = ['crocodile', 'elephant', 'llama', 'snake']
    animal_poses = {}
    from sklearn import linear_model
    for animal in animals:
        data_animal = [d for d in all_bearings if d['animal'] == animal]
        data = np.asarray([[d['pose'][0][0], d['pose'][1][0], d['pose'][2][0], d['bearing']] for d in data_animal])
        L = triangulate_animal(data)
        #A, B = triangulate_animal(data)
        #ransac = linear_model.RANSACRegressor()
        #ransac.fit(A, B)
        #pose_animal = ransac.get_params()
        #print(pose_animal)
        animal_poses[animal] = L
        print('animal {}, x:{},y:{}'.format(animal, L[0], L[1]))


    # plot transformed map and locations of animals 
    import matplotlib.pyplot as plt
    markers1 = np.vstack([slam1.markers, np.ones(len(slam1.markers[0]))])
    #markers2 = np.vstack([slam2.markers, np.ones(len(slam2.markers[0]))])
    #markers3 = np.vstack([slam3.markers, np.ones(len(slam3.markers[0]))])

    #markers2_t = f1Tf2 @ markers2
    #markers3_t = f1Tf3 @ markers3

    plt.scatter(markers1[0], markers1[1], label='map1')
    plt.show()
    for key, value in animal_poses.items():
        plt.scatter(value[0], value[1], label=key)
    plt.legend()
    plt.show()

