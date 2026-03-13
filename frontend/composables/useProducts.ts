import type { Product, StockUpdatePayload } from '~/types'

export const useProducts = () => {
  const client = useSupabaseClient()

  const {
    data: products,
    pending,
    error,
    refresh,
  } = useAsyncData('products', async () => {
    const { data, error } = await client
      .from('products')
      .select('*')
      .order('name')

    if (error) throw error
    return data as Product[]
  })

  const fetchProduct = async (id: string): Promise<Product | null> => {
    const { data, error } = await client
      .from('products')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as Product
  }

  const updateStockCount = async (payload: StockUpdatePayload) => {
    const { error } = await client
      .from('products')
      .update({
        stock_count: payload.stock_count,
        updated_at: new Date().toISOString(),
      })
      .eq('id', payload.id)

    if (error) throw error
    await refresh()
  }

  return { products, pending, error, refresh, fetchProduct, updateStockCount }
}
