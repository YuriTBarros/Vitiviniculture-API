import asyncio

from api.services import category_service


async def periodic_sync_job():
    while True:
        try:
            print("[SYNC] Starting exportation sync...")
            await category_service.sync("exportation")

            print("[SYNC] Starting importation sync...")
            await category_service.sync("importation")

            print("[SYNC] Starting processing sync...")
            await category_service.sync("processing")

            print("[SYNC] Starting production sync...")
            await category_service.sync("production")

            print("[SYNC] Starting trade sync...")
            await category_service.sync("trade")
        except Exception as e:
            print(f"[SYNC-ERROR] Sync failed: {e}")
        print("[SYNC] Waiting 10 minutes before next sync...")
        await asyncio.sleep(600)  # 10 minutes
