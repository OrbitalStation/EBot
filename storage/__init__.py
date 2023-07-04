from database.interface import CloudStorage


CLOUD_STORAGE_BUTTONS = [ty.__name__ for field, ty in
                         CloudStorage.__annotations__.items() if field != "preferred"]
