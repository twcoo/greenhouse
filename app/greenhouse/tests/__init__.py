from .auth import AuthLoginTests, AuthLogoutTests, AuthRegisterTests
from .crops import (CropCreateApiViewTests, CropDeleteApiViewTests,
                    CropGetApiViewTests, CropImageUploadApiViewTests,
                    CropListApiViewTests, CropPartialUpdateApiViewTests,
                    CropUpdateApiViewTests)

__all__ = [
    "AuthLoginTests",
    "AuthLogoutTests",
    "AuthRegisterTests",
    "CropCreateApiViewTests",
    "CropDeleteApiViewTests",
    "CropGetApiViewTests",
    "CropListApiViewTests",
    "CropPartialUpdateApiViewTests",
    "CropUpdateApiViewTests",
    "CropImageUploadApiViewTests",
]
