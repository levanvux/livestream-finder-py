import pandas as pd

from database.livestream_repository import get_all_events


def export_to_excel(filename="livestreams.xlsx"):
    events = get_all_events()

    rows = [dict(row._mapping) for row in events]

    df = pd.DataFrame(rows)

    df = df.drop(columns=["id"])

    df = df.rename(
        columns={
            "id": "ID",
            "title": "Tiêu đề",
            "platform": "Nền tảng",
            "description": "Mô tả",
            "url": "Link",
            "keyword": "Từ khóa",
            "start_time": "Thời gian bắt đầu",
            "score": "Điểm tiềm năng",
            "industry": "Ngành nghề",
            "language": "Ngôn ngữ",
            "buyer_persona": "Khách hàng mục tiêu",
            "suggested_comment": "Bình luận được gửi vào livestream",
            "created_at": "Ngày tạo",
        }
    )

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Livestreams", index=True)

        ws = writer.sheets["Livestreams"]

        # Freeze hàng tiêu đề
        ws.freeze_panes = "A2"

        # Auto Filter
        ws.auto_filter.ref = ws.dimensions

        # Độ rộng từng cột
        column_widths = {
            "A": 6,  # Index
            "B": 40,  # Tiêu đề
            "C": 15,  # Nền tảng
            "D": 60,  # Mô tả
            "E": 40,  # Link
            "F": 15,  # Từ khóa
            "G": 25,  # Thời gian bắt đầu
            "H": 15,  # Điểm
            "I": 35,  # Ngành
            "J": 20,  # Ngôn ngữ
            "K": 40,  # Buyer Persona
            "L": 60,  # Comment
            "M": 25,  # Ngày tạo
        }

        for col, width in column_widths.items():
            ws.column_dimensions[col].width = width

    print(f"✅ Exported {len(df)} records -> {filename}")


if __name__ == "__main__":
    export_to_excel()
