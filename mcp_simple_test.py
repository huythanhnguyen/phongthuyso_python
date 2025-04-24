"""
Chạy thử MCP đơn giản
"""

import asyncio

# Lớp cơ sở cho các agent
class Agent:
    def __init__(self, name):
        self.name = name
        
    async def process(self, message):
        print(f"[{self.name}] Đang xử lý: {message}")
        return f"Kết quả từ {self.name}: Đã xử lý '{message}'"

# Root agent
class RootAgent(Agent):
    def __init__(self):
        super().__init__("root_agent")
        self.sub_agents = {}
        
    def add_sub_agent(self, name, agent):
        self.sub_agents[name] = agent
        
    async def process(self, message):
        print(f"[{self.name}] Đang xử lý: {message}")
        
        # Chuyển hướng đến agent phù hợp
        if "số điện thoại" in message.lower():
            print(f"[{self.name}] Chuyển đến batcuclinh_so_agent")
            return await self.sub_agents["batcuclinh_so_agent"].process(message)
        elif "thanh toán" in message.lower():
            print(f"[{self.name}] Chuyển đến payment_agent")
            return await self.sub_agents["payment_agent"].process(message)
        else:
            return f"Kết quả từ {self.name}: Đã xử lý '{message}'"

# Sub agents
class BatCucLinhSoAgent(Agent):
    def __init__(self):
        super().__init__("batcuclinh_so_agent")
        
    async def process(self, message):
        print(f"[{self.name}] Đang xử lý: {message}")
        return f"Kết quả từ {self.name}: Phân tích số điện thoại trong '{message}'"

class PaymentAgent(Agent):
    def __init__(self):
        super().__init__("payment_agent")
        
    async def process(self, message):
        print(f"[{self.name}] Đang xử lý: {message}")
        return f"Kết quả từ {self.name}: Xử lý thanh toán từ '{message}'"

# Hàm chính
async def main():
    print("=== Bắt đầu chạy thử MCP ===")
    
    # Khởi tạo các agent
    root = RootAgent()
    batcuclinh_so = BatCucLinhSoAgent()
    payment = PaymentAgent()
    
    # Đăng ký sub agents
    root.add_sub_agent("batcuclinh_so_agent", batcuclinh_so)
    root.add_sub_agent("payment_agent", payment)
    
    # Danh sách tin nhắn thử nghiệm
    messages = [
        "Xin chào, tôi cần giúp đỡ",
        "Phân tích số điện thoại 0912345678",
        "Tôi muốn thanh toán dịch vụ"
    ]
    
    # Xử lý các tin nhắn
    for msg in messages:
        print(f"\n--- Tin nhắn: {msg} ---")
        result = await root.process(msg)
        print(f"Kết quả: {result}")
    
    print("\n=== Hoàn thành thử nghiệm MCP ===")

# Điểm bắt đầu
print("Script bắt đầu chạy")
if __name__ == "__main__":
    print("Đang gọi hàm main...")
    asyncio.run(main())
    print("Hàm main đã hoàn thành") 