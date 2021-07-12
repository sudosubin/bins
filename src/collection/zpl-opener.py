import asyncio

from package import Package
from package.source import PackageSource


class ZplOpener(Package):
    name = 'zpl-opener'
    description = 'Open zeplin app uri in your default browser'

    repo = 'sudosubin/zeplin-uri-opener'
    source = PackageSource.GITHUB_TAG

    bin_pattern = ['./*/src/zpl-open']
    link_pattern = {
        './*/src/zpl-open': '$BIN_DIR/zpl-open',
        './*/src/zpl-opener.desktop': '~/.local/share/applications/zpl-opener.desktop'
    }

    async def postinstall(self):
        proc = await asyncio.create_subprocess_shell('xdg-mime default zpl-opener.desktop x-scheme-handler/zpl',
                                                     stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)

        await proc.wait()
