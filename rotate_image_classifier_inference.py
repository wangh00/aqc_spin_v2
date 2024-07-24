import os

import numpy as np
import torch
import torch.nn as nn
from torchvision import models
from utils import RotNetDataset
import torch.nn.functional as F

input_shape = (3, 244, 244)


class RotateNet(nn.Module):

    def __init__(self):
        super().__init__()
        self.model = models.resnet50(pretrained=True)
        self.model.fc = nn.Linear(2048, 360)

    def forward(self, x):
        """
        前向传播，使用resnet 50作为backbone，后面接一个线性层。

        Args:
            x (_type_): (batch, 3, 224, 224)

        Returns:
            _type_: 360维的一个tensor，表征属于每一个角度类别的概率
        """
        x = self.model(x)

        return x


def get_result(data_path):
    with torch.no_grad():
        model = torch.load('models/model_13.pth', map_location=torch.device('cpu')).eval()
        # data_path = './img_examples'
        files = os.listdir(data_path)
        labels = [file.split('.')[0].split('_')[1] for file in files]
        files = [os.path.join(data_path, f) for f in files]
        val_dataset = RotNetDataset(files, input_shape=input_shape, rotate=False)
        val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=64)
        for (img, rotate_angle), label in zip(val_dataloader, labels):
            img = img.float()
            logits = model(img)
            logits = F.softmax(logits, dim=-1)
            pred = np.argmax(logits.numpy(), axis=1)
        avg_diff = 0
        result = []
        for p, l in zip(pred, labels):
            result.append({'Infer': p, 'Label': l})
        return result, avg_diff


# page=d.page
# img=page.ele('c:.passMod_spin-background')
# img.get_screenshot()
# bytes_str = img.get_screenshot(as_bytes='png')
# with open('test/driss_test.png','wb') as f:
#     f.write(bytes_str)
# 滑动系数0.68
# result = get_result('img_file')
# print(result)
if __name__ == '__main__':
    result = get_result('img_file')
    print(result)
