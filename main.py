from code.menu import Menu
import asyncio

async def main():
    # game = ChessReboot()
    # game.run()
    menu = Menu()
    await menu.run()
    # pygame.quit()
    
asyncio.run(main())