import type { DetectionLog } from '~/types'

export const useDetectionLogs = () => {
  const client = useSupabaseClient()

  const fetchLatestByProductIds = async (
    productIds: string[]
  ): Promise<Map<string, DetectionLog>> => {
    if (productIds.length === 0) return new Map()

    const { data, error } = await client
      .from('detection_logs')
      .select('*')
      .in('product_id', productIds)
      .order('detected_at', { ascending: false })

    if (error) throw error

    const map = new Map<string, DetectionLog>()
    for (const log of (data as DetectionLog[])) {
      if (!map.has(log.product_id)) {
        map.set(log.product_id, log)
      }
    }
    return map
  }

  const fetchByProductId = async (
    productId: string,
    limit = 50
  ): Promise<DetectionLog[]> => {
    const { data, error } = await client
      .from('detection_logs')
      .select('*')
      .eq('product_id', productId)
      .order('detected_at', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data as DetectionLog[]
  }

  return { fetchLatestByProductIds, fetchByProductId }
}
