from HelperClasses.GenericViewsFolder.GetGenerics import GetView
from HelperClasses.GenericViewsFolder.PostGenerics import PostView
from HelperClasses.GenericViewsFolder.PutGenerics import PutView
from HelperClasses.GenericViewsFolder.PatchGenerics import PatchView
from HelperClasses.GenericViewsFolder.DeleteGenerics import DeleteView


class CRUDView(GetView, PostView, PutView, DeleteView, PatchView):
    pass


class CRUView(GetView, PostView, PutView, PatchView):
    pass
