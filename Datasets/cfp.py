import os
import cv2
import numpy as np
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader

def image_loader(image_path):
    try:
        image = cv2.imread(image_path)
        if len(image.shape) == 2:
            image = np.stack([image]*3, 2)
        return image
    except IOError:
        print('fail to load image:' + image_path)

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean = (0.5, 0.5, 0.5), std = (0.5, 0.5, 0.5))
])

class CFP_FP(Dataset):
    def __init__(self, root, file_list):

        self.root = root
        self.file_list = file_list
        self.nameLs = []
        self.nameRs = []
        self.folds = []
        self.labels = []

        with open(file_list) as f:
            pairs = f.read().splitlines()
        for i, p in enumerate(pairs):
            p = p.split(' ')
            nameL = p[0]
            nameR = p[1]
            fold = i // 700
            label = int(p[2])

            self.nameLs.append(nameL)
            self.nameRs.append(nameR)
            self.folds.append(fold)
            self.labels.append(label)

    def __getitem__(self, index):

        img_l = image_loader(os.path.join(self.root, self.nameLs[index]))
        img_r = image_loader(os.path.join(self.root, self.nameRs[index]))
        image_list = [img_l, cv2.flip(img_l, 1), img_r, cv2.flip(img_r, 1)]

        for i in range(len(image_list)):
            image_list[i] = transform(image_list[i])

        return image_list

    def __len__(self):
        return len(self.nameLs)

if __name__ == '__main__':
    dataset_path = '/data/face_datasets/test_datasets/face_verification/CFP-FP/CFP_FP_aligned_112'
    file_list = '/data/face_datasets/test_datasets/face_verification/CFP-FP/cfp_fp_pair.txt'

    cfp_dataset = CFP_FP(dataset_path, file_list)
    cfp_dataloader = DataLoader(cfp_dataset, batch_size=128, shuffle=False, num_workers=4, drop_last=False)
    print(len(cfp_dataset))
    print(len(cfp_dataloader))
    for data in cfp_dataloader:
        print(len(data))