import abc
import warnings

import torch


class BasicTransform(abc.ABC):
    """
    Transforms are applied to each sample individually. The dataloader is responsible for collating, or we might consider a CollateTransform

    We expect (C, X, Y) or (C, X, Y, Z) shaped inputs for image and seg (yes seg can have more color channels)

    No idea what keypoint and bbox will look like, this is Michaels turf
    """
    def __init__(self):
        pass

    def __call__(self, **data_dict) -> dict:
        params = self.get_parameters(**data_dict)
        return self.apply(data_dict, **params)

    def apply(self, data_dict, **params):
        if data_dict.get('image') is not None:
            data_dict['image'] = self._apply_to_image(data_dict['image'], **params)

        if data_dict.get('segmentation') is not None:
            data_dict['segmentation'] = self._apply_to_segmentation(data_dict['segmentation'], **params)

        if data_dict.get('keypoints') is not None:
            data_dict['keypoints'] = self._apply_to_keypoints(data_dict['keypoints'], **params)

        if data_dict.get('bbox') is not None:
            data_dict['bbox'] = self._apply_to_bbox(data_dict['bbox'], **params)

        return data_dict

    def _apply_to_image(self, img: torch.Tensor, **params) -> torch.Tensor:
        pass

    def _apply_to_segmentation(self, segmentation: torch.Tensor, **params) -> torch.Tensor:
        pass

    def _apply_to_keypoints(self, keypoints, **params):
        pass

    def _apply_to_bbox(self, bbox, **params):
        pass

    @abc.abstractmethod
    def get_parameters(self, **data_dict) -> dict:
        pass


class RandomTransform(BasicTransform):
    def __init__(self, transform: BasicTransform, apply_probability: float = 1):
        super().__init__()
        self.transform = transform
        self.apply_probability = apply_probability

    def get_parameters(self, **data_dict) -> dict:
        return {"apply_transform": torch.rand(1).item() < self.apply_probability}

    def apply(self, data_dict: dict, **params) -> dict:
        if params['apply_to_sample']:
            return self.transform(**data_dict)
        else:
            return data_dict


class ImageOnlyTransform(BasicTransform):
    def apply(self, data_dict: dict, **params) -> dict:
        if data_dict.get('image') is not None:
            data_dict['image'] = self._apply_to_image(data_dict['image'], **params)
        return data_dict


class SegOnlyTransform(BasicTransform):
    def apply(self, data_dict: dict, **params) -> dict:
        if data_dict.get('segmentation') is not None:
            data_dict['segmentation'] = self._apply_to_image(data_dict['segmentation'], **params)
        return data_dict


if __name__ == '__main__':
    pass