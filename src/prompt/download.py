from rich.progress import Progress

from utils.request import request


async def download():
    with Progress() as progress:
        task = progress.add_task("[red]Downloading...", total=100.0)
        task2 = progress.add_task("[red]Down...", total=100.0)

        async with request.session.get(endpoint, headers=get_headers(), chunked=False) as resp:
            # print(resp.status)
            # print(resp.raw_headers)
            # content_length = resp.headers.get('content-length')
            # print(content_length)

            async for chunk in resp.content.iter_chunked(1024):
                progress.update(task, advance=len(chunk))
                pass
                # print(len(chunk))
