from commands.__helper import setter


@setter(
    "google_disk_client_secrets",
    "botHumanGDClientSecrets",
    extra_info_key="botSetGDClientSecretsExtraInfo",
    info_attachment_path="googleCloudAccountGuidePath")
def command(_new):
    return True
