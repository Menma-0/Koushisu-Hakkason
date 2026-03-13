import cv2
import time
from ultralytics import YOLO
from supabase import create_client, Client
import os

# 1. Supabaseの設定（ダッシュボードのProject Settings > APIから取得）
SUPABASE_URL = "https://pjzikvqgnklcpptkvvay.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqemlrdnFnbmtsY3BwdGt2dmF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI5MjU5NDYsImV4cCI6MjA4ODUwMTk0Nn0.fBsG46bdwCte5oDno4GnqVhDfNF2Ub0RL4BBzitQSJc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. YOLOモデルの読み込み ---
model = YOLO("yolov8n.pt")

# --- 3. カメラの設定 ---
cap = cv2.VideoCapture(0)

# 記録対象の商品のID (productsテーブルの id:1 と紐付けます)
TARGET_PRODUCT_ID = 1  

last_upload_time = 0
upload_interval = 10  # 履歴なので、例えば10秒に1回記録

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
        # 何も映っていない時も「0個だった」という記録を残すならこのまま
        # 何か映っている時だけ残したいなら if current_shelf_count > 0: を追加
        
        data = {
            "product_id": TARGET_PRODUCT_ID,  # どの商品のログか
            "shelf_count": current_shelf_count, # その時の棚の数
            "image_url": None,                 # 画像機能を使うまでは空
            # detected_at はDB側で default now() なら自動設定されます
        }
        
        try:
            # .insert() を使うことで、新しい行が追加される
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