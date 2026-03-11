from .auth import AuthLoginTests, AuthLogoutTests
from .crops import (CropCreateApiViewTests, CropDeleteApiViewTests,
                    CropGetApiViewTests, CropImageUploadApiViewTests,
                    CropListApiViewTests, CropPartialUpdateApiViewTests,
                    CropUpdateApiViewTests)
from .setup import SetupAdminTests, SetupStatusTests

__all__ = [
    "SetupAdminTests",
    "SetupStatusTests",
    "AuthLoginTests",
    "AuthLogoutTests",
    "CropCreateApiViewTests",
    "CropDeleteApiViewTests",
    "CropGetApiViewTests",
    "CropListApiViewTests",
    "CropPartialUpdateApiViewTests",
    "CropUpdateApiViewTests",
    "CropImageUploadApiViewTests",
]
