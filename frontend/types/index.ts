/** products テーブルの行 */
export interface Product {
  id: string
  name: string
  shelf_max: number
  stock_max: number
  stock_count: number
  image_url: string | null
  created_at: string
  updated_at: string
}

/** detection_logs テーブルの行 */
export interface DetectionLog {
  id: string
  product_id: string
  shelf_count: number
  image_url: string | null
  detected_at: string
}

/** 緊急度レベル */
export type UrgencyLevel = 'danger' | 'warning' | 'safe'

/** 最新検知データと算出値を付与した商品 */
export interface ProductWithStatus extends Product {
  latestDetection: DetectionLog | null
  shelfCount: number
  replenishCount: number
  stockRatio: number
  urgency: UrgencyLevel
}

/** stock_count 更新用ペイロード */
export interface StockUpdatePayload {
  id: string
  stock_count: number
}
