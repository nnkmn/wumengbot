import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// API接口定义
export const api = {
  // 玩家相关
  searchPlayer: (params) => apiClient.get('/players/search', { params }),
  
  // 成绩相关
  getPlayerScores: (params) => apiClient.get('/scores/player', { params }),
  
  // 歌曲相关
  getAllSongs: () => apiClient.get('/songs'),
  getSongById: (id) => apiClient.get(`/songs/id/${id}`),
  searchSongs: (params) => apiClient.get('/songs/search', { params }),
  
  // 牌子相关
  getPlayerPlates: (params) => apiClient.get('/plates/player', { params }),
  
  // Segamaid相关
  bindSegamaid: (data) => apiClient.post('/segamaid/bind', data)
}
