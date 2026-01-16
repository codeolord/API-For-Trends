import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const trendsApi = {
  list: (skip = 0, limit = 20, filters?: any) =>
    api.get('/trends', { params: { skip, limit, ...filters } }),
  get: (id: number) => api.get(`/trends/${id}`),
  create: (data: any) => api.post('/trends', data),
}

export const productsApi = {
  list: (skip = 0, limit = 20, filters?: any) =>
    api.get('/products', { params: { skip, limit, ...filters } }),
  get: (id: number) => api.get(`/products/${id}`),
  create: (data: any) => api.post('/products', data),
}

export const designsApi = {
  list: (skip = 0, limit = 20, filters?: any) =>
    api.get('/designs', { params: { skip, limit, ...filters } }),
  get: (id: number) => api.get(`/designs/${id}`),
  create: (data: any) => api.post('/designs', data),
}

export default api
