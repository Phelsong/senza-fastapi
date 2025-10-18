#!pyscript
# libs
from asyncio import ensure_future
from pyscript import config
from pyscript.web import page

# imports
from senza.dom_router import dom_router
from senza.context import site
from web.views.test_page import test_page


# =======================
async def main() -> None:
    # ==================================
    await dom_router.add(test_page)
    print(await dom_router.routes)
    await dom_router.nav("/test_page")
    # ==================================


ensure_future(main())
# await main()
