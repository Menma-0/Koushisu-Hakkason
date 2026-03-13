import cv2
import time
import os
from ultralytics import YOLO
from supabase import create_client, Client
from dotenv import load_dotenv  # 追加: dotenvをインポート
from pathlib import Path        # 追加: Pathをインポート

# --- 1. 環境変数の読み込み ---
# 今のファイルの場所（pytqqhon-service内）を取得
current_dir = Path(__file__).resolve().parent

# 一つ上の階層（ルート）にある .env ファイルのパスを作る
env_path = current_dir.parent / '.env'

# 指定したパスから環境変数を読み込む
load_dotenv(dotenv_path=env_path)

# 環境変数を参照する（変数名を統一します）
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Supabaseクライアントの作成
if not SUPABASE_URL or not SUPABASE_KEY:
    print("エラー: .envファイルからURLまたはKEYが読み込めませんでした。")
    exit()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. YOLOモデルの読み込み ---
model = YOLO("yolov8n.pt")

# --- 3. カメラの設定 ---
cap = cv2.VideoCapture(0)

# 記録対象の商品のID (productsテーブルの id:1 と紐付けます)
TARGET_PRODUCT_ID = 1  

last_upload_time = 0
upload_interval = 10  # 10秒に1回記録

print(f"実行中... detection_logs に商品ID:{TARGET_PRODUCT_ID} の検知履歴を保存します")
print("'q'キーで終了")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # YOLOで物体検出
    results = model(frame, conf=0.5)
    
    # 今、棚（カメラ）に映っている数
    current_shelf_count = len(results[0].boxes)

    current_time = time.time()
    
    # 10秒ごとに履歴を1件追加（INSERT）
    if current_time - last_upload_time > upload_interval:
        data = {
            "product_id": TARGET_PRODUCT_ID,
            "shelf_count": current_shelf_count,
            "image_url": None,
        }
        
q        try:
            response = supabase.table("detection_logs").insert(data).execute()
            print(f"【履歴保存】時刻: {time.strftime('%H:%M:%S')} | 商品数: {current_shelf_count}個 を記録しました")
            last_upload_time = current_time
        except Exception as e:
            print(f"【エラー】保存失敗: {e}")

    # 確認用のプレビュー画面
    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Detection Log Mode", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()