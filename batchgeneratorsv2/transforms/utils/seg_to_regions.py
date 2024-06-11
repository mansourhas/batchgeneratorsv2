from typing import Union, List, Tuple
import torch

from batchgeneratorsv2.transforms.base.basic_transform import SegOnlyTransform


class ConvertSegmentationToRegionsTransform(SegOnlyTransform):
    def __init__(self, regions: Union[List, Tuple], channel_in_seg: int = 0):
        super().__init__()
        self.regions = [torch.Tensor(i) if not isinstance(i, int) else torch.Tensor([i]) for i in regions]
        self.channel_in_seg = channel_in_seg

    def _apply_to_segmentation(self, segmentation: torch.Tensor, **params) -> torch.Tensor:
        num_regions = len(self.regions)
        region_output = torch.zeros((num_regions, *segmentation.shape[1:]), dtype=torch.bool, device=segmentation.device)
        for region_id, region_labels in enumerate(self.regions):
            if isinstance(region_labels, int) or len(region_labels) == 1:
                if not isinstance(region_labels, int):
                    region_labels = region_labels[0]
                region_output[:, region_id] = segmentation[:, self.channel_in_seg] == region_labels
            else:
                region_output[:, region_id] |= torch.isin(segmentation[:, self.channel_in_seg], torch.tensor(region_labels).to(segmentation.dtype))
        return region_output.to(segmentation.dtype)


