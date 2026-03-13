import type {
  Product,
  DetectionLog,
  ProductWithStatus,
  UrgencyLevel,
} from '~/types'

export const useInventoryStatus = () => {
  const computeUrgency = (
    shelfCount: number,
    shelfMax: number,
    stockCount: number,
    stockMax: number
  ): UrgencyLevel => {
    if (shelfCount === 0) return 'danger'

    const stockRatio = stockMax > 0 ? stockCount / stockMax : 0
    if (stockRatio < 0.2) return 'danger'
    if (stockRatio <= 0.5) return 'warning'
    return 'safe'
  }

  const enrichProduct = (
    product: Product,
    latestDetection: DetectionLog | null
  ): ProductWithStatus => {
    const shelfCount = latestDetection?.shelf_count ?? 0
    const stockRatio = product.stock_max > 0
      ? product.stock_count / product.stock_max
      : 0

    return {
      ...product,
      latestDetection,
      shelfCount,
      replenishCount: Math.max(0, product.shelf_max - shelfCount),
      stockRatio,
      urgency: computeUrgency(
        shelfCount,
        product.shelf_max,
        product.stock_count,
        product.stock_max
      ),
    }
  }

  const enrichProducts = (
    products: Product[],
    latestDetections: Map<string, DetectionLog>
  ): ProductWithStatus[] => {
    return products.map((p) =>
      enrichProduct(p, latestDetections.get(p.id) ?? null)
    )
  }

  const urgencyColor = (urgency: UrgencyLevel): string => {
    const map: Record<UrgencyLevel, string> = {
      danger: 'red',
      warning: 'orange',
      safe: 'blue',
    }
    return map[urgency]
  }

  const urgencyLabel = (urgency: UrgencyLevel): string => {
    const map: Record<UrgencyLevel, string> = {
      danger: '要補充',
      warning: '注意',
      safe: '正常',
    }
    return map[urgency]
  }

  return {
    computeUrgency,
    enrichProduct,
    enrichProducts,
    urgencyColor,
    urgencyLabel,
  }
}
