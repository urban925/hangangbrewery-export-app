import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

interface Company {
  id: number
  original: string
  normalized: string
}

interface Product {
  id: number
  original: string
  normalized: string
}

interface MasterList {
  companies: Company[]
  products: Product[]
}

function App() {
  const [masterList, setMasterList] = useState<MasterList | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // 백엔드 API에서 마스터 리스트 조회
    axios.get('http://localhost:8000/api/master-lists')
      .then(response => {
        setMasterList(response.data)
        setLoading(false)
      })
      .catch(err => {
        setError('API 호출 실패: ' + err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div style={{ padding: '20px' }}>
      <h1>한강주조 출고표 자동화</h1>
      
      {loading && <p>로딩 중...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {masterList && (
        <div>
          <h2>마스터 리스트</h2>
          <p>✅ 등록된 업체: {masterList.companies.length}개</p>
          <p>✅ 등록된 상품: {masterList.products.length}개</p>
          
          <hr />
          
          <h3>업체 목록 (처음 5개)</h3>
          <ul>
            {masterList.companies.slice(0, 5).map(company => (
              <li key={company.id}>{company.normalized}</li>
            ))}
          </ul>
          
          <h3>상품 목록 (처음 5개)</h3>
          <ul>
            {masterList.products.slice(0, 5).map(product => (
              <li key={product.id}>{product.normalized}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App