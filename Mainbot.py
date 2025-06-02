import nextcord
from nextcord.ext import commands
import os
import asyncio # Thường cần thiết cho các tác vụ bot
from datetime import datetime # Để khởi tạo next_shop_restock_time

# --- Cấu hình Bot Cơ bản ---
BOT_TOKEN = "MTM3ODkyNTU4MzI2MTc2NTc5Mg.GSBhO_.jBNTwGWDR7-imV705wqjEY-Phf8iBJmUj4cgtQ"
COMMAND_PREFIX = "!" # Bạn có thể thay đổi prefix nếu muốn

# --- Khởi tạo Intents ---
intents = nextcord.Intents.default()
intents.message_content = True # Cần để đọc nội dung tin nhắn (cho lệnh prefix và lệnh tắt)
intents.members = True       # Cần để lấy thông tin thành viên (ví dụ: khi tag user)

# --- Khởi tạo Bot Instance ---
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# --- Khởi tạo các thuộc tính toàn cục cho bot (Cogs sẽ truy cập qua self.bot) ---
# Các thuộc tính này sẽ được quản lý và cập nhật bởi các Cogs tương ứng.
bot.current_dynamic_shop_items = {}  # Sẽ chứa các vật phẩm ngẫu nhiên trong shop
bot.next_shop_restock_time = datetime.now() # Thời điểm restock shop tiếp theo
bot.ALL_ITEM_METADATA = {} # Sẽ chứa thông tin metadata của tất cả vật phẩm (emoji, tên VN, giá bán, v.v.)


@bot.event
async def on_ready():
    """
    Sự kiện được kích hoạt khi bot đã kết nối thành công với Discord 
    và sẵn sàng nhận lệnh.
    """
    print("-" * 30)
    print(f'Đã đăng nhập với tên: {bot.user.name} (ID: {bot.user.id})')
    print(f'Nextcord Version: {nextcord.__version__}')
    print(f'Prefix lệnh hiện tại: {COMMAND_PREFIX}')
    print(f'Sẵn sàng hoạt động trên {len(bot.guilds)} server(s).')
    print("-" * 30)
    
    # Tải các Cogs (extensions)
    # Hàm populate_all_item_metadata(bot) và việc khởi động shop_restock_task
    # sẽ được xử lý bên trong một Cog (ví dụ: một Cog quản lý sự kiện hoặc Cog quản lý shop)
    # sau khi Cog đó được tải.
    
    print("Đang tải các Cogs...")
    loaded_cogs_count = 0
    cogs_path = './cogs' # Giả sử các Cogs nằm trong thư mục 'cogs' cùng cấp với bot_main.py

    if not os.path.exists(cogs_path):
        os.makedirs(cogs_path)
        print(f"Đã tạo thư mục '{cogs_path}' vì nó chưa tồn tại.")
        print("Vui lòng đặt các file Cog của bạn vào thư mục này.")

    for filename in os.listdir(cogs_path):
        if filename.endswith('.py') and not filename.startswith('_'): # Bỏ qua file như __init__.py
            extension_name = f'cogs.{filename[:-3]}'
            try:
                bot.load_extension(extension_name)
                print(f'✅ Đã tải thành công Cog: {extension_name}')
                loaded_cogs_count += 1
            except commands.ExtensionNotFound:
                print(f'⚠️ Không tìm thấy Cog: {extension_name}. Đảm bảo file tồn tại và đúng đường dẫn.')
            except commands.NoEntryPointError:
                print(f'⛔ LỖI: Cog {extension_name} thiếu hàm setup().')
            except commands.ExtensionFailed as e:
                print(f'⛔ LỖI khi tải Cog {extension_name}: {e.__class__.__name__} - {e}')
            except Exception as e:
                print(f'⛔ LỖI không xác định khi tải Cog {extension_name}: {type(e).__name__} - {e}')
                
    if loaded_cogs_count > 0:
        print(f"--- Đã tải {loaded_cogs_count} Cog(s) ---")
    else:
        print("--- Không có Cog nào được tải. Bot có thể không có nhiều lệnh. ---")

    # Đặt trạng thái cho bot (tùy chọn)
    await bot.change_presence(activity=nextcord.Game(name=f"với {COMMAND_PREFIX}help | /help"))

if __name__ == "__main__":
    print("Đang khởi động bot...")
    if BOT_TOKEN == "MTM3ODkyNTU4MzI2MTc2NTc5Mg.GSBhO_.jBNTwGWDR7-imV705wqjEY-Phf8iBJmUj4cgtQ" or \
       BOT_TOKEN == "TOKEN_CUA_BAN" or \
       not BOT_TOKEN:
        print("CẢNH BÁO: Bạn đang sử dụng token mặc định hoặc token rỗng.")
        print("Vui lòng cập nhật BOT_TOKEN trong file bot_main.py với token bot Discord của bạn.")
        # Có thể thêm input() để người dùng xác nhận hoặc thoát nếu muốn
        # user_input = input("Nhấn Enter để tiếp tục với token này (KHÔNG KHUYẾN KHÍCH) hoặc đóng cửa sổ để thoát...")
        # if not user_input: # Nếu người dùng chỉ nhấn Enter
        #     pass
    
    try:
        bot.run(BOT_TOKEN)
    except nextcord.errors.LoginFailure:
        print("LỖI ĐĂNG NHẬP: Token không hợp lệ hoặc đã bị thu hồi. Hãy kiểm tra lại BOT_TOKEN.")
    except Exception as e:
        print(f"LỖI KHÔNG XÁC ĐỊNH KHI CHẠY BOT: {type(e).__name__} - {e}")

