import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [filters, setFilters] = useState({ min_price: 0, max_price: 100000, min_rating: 0, brand: '', category: '' });
  const [compareList, setCompareList] = useState([]);
  const [showCompare, setShowCompare] = useState(false);
  const [loading, setLoading] = useState(false);

  const categories = ['Electronics', 'Clothing', 'Books', 'Appliances', 'Sports'];

  const search = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/api/search`, { params: { q: query, ...filters } });
      setProducts(res.data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  useEffect(() => { search(); }, []);

  const toggleCompare = (product) => {
    setCompareList(prev =>
      prev.find(p => p.product_id === product.product_id)
        ? prev.filter(p => p.product_id !== product.product_id)
        : prev.length < 4 ? [...prev, product] : prev
    );
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🛒 ShopSmart — Intelligent Product Search</h1>
      </header>

      <div className="search-bar">
        <input
          type="text"
          placeholder='Search products e.g. "wireless headphones under 2000"'
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && search()}
        />
        <button onClick={search} className="btn-search">Search</button>
      </div>

      <div className="main-layout">
        <aside className="filters">
          <h3>Filters</h3>
          <label>Category</label>
          <select value={filters.category} onChange={e => setFilters({ ...filters, category: e.target.value })}>
            <option value="">All</option>
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>

          <label>Brand</label>
          <input placeholder="e.g. Sony" value={filters.brand} onChange={e => setFilters({ ...filters, brand: e.target.value })} />

          <label>Min Price: ₹{filters.min_price}</label>
          <input type="range" min="0" max="100000" step="500" value={filters.min_price} onChange={e => setFilters({ ...filters, min_price: Number(e.target.value) })} />

          <label>Max Price: ₹{filters.max_price}</label>
          <input type="range" min="0" max="100000" step="500" value={filters.max_price} onChange={e => setFilters({ ...filters, max_price: Number(e.target.value) })} />

          <label>Min Rating: {filters.min_rating}⭐</label>
          <input type="range" min="0" max="5" step="0.5" value={filters.min_rating} onChange={e => setFilters({ ...filters, min_rating: Number(e.target.value) })} />

          <button className="btn-apply" onClick={search}>Apply Filters</button>
          <button className="btn-clear" onClick={() => { setFilters({ min_price: 0, max_price: 100000, min_rating: 0, brand: '', category: '' }); setQuery(''); }}>Clear</button>
        </aside>

        <main className="products">
          {compareList.length > 0 && (
            <div className="compare-bar">
              <span>{compareList.length} items selected for comparison</span>
              <button onClick={() => setShowCompare(true)} className="btn-compare">Compare Now</button>
              <button onClick={() => setCompareList([])} className="btn-clear-compare">Clear</button>
            </div>
          )}

          {loading ? <p>Loading...</p> : (
            <div className="product-grid">
              {products.map(p => {
                const inCompare = compareList.find(c => c.product_id === p.product_id);
                return (
                  <div key={p.product_id} className={`product-card ${inCompare ? 'selected' : ''}`}>
                    <div className="product-category">{p.category}</div>
                    <h3>{p.name}</h3>
                    <p className="brand">{p.brand}</p>
                    <p className="description">{p.description}</p>
                    <div className="product-footer">
                      <span className="price">₹{p.price.toLocaleString()}</span>
                      <span className="rating">⭐ {p.rating}</span>
                    </div>
                    <button className={`btn-add-compare ${inCompare ? 'added' : ''}`} onClick={() => toggleCompare(p)}>
                      {inCompare ? '✓ Added' : '+ Compare'}
                    </button>
                  </div>
                );
              })}
              {products.length === 0 && <p className="no-results">No products found. Try a different search.</p>}
            </div>
          )}
        </main>
      </div>

      {showCompare && (
        <div className="compare-modal">
          <div className="compare-content">
            <h2>Price Comparison</h2>
            <button className="close-btn" onClick={() => setShowCompare(false)}>✕</button>
            <table>
              <thead>
                <tr>
                  <th>Feature</th>
                  {compareList.map(p => <th key={p.product_id}>{p.name}</th>)}
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Price</td>
                  {compareList.map(p => {
                    const cheapest = Math.min(...compareList.map(x => x.price));
                    return <td key={p.product_id} className={p.price === cheapest ? 'cheapest' : ''}>₹{p.price.toLocaleString()} {p.price === cheapest ? '✓ Best' : ''}</td>;
                  })}
                </tr>
                <tr><td>Brand</td>{compareList.map(p => <td key={p.product_id}>{p.brand}</td>)}</tr>
                <tr><td>Rating</td>{compareList.map(p => <td key={p.product_id}>⭐ {p.rating}</td>)}</tr>
                <tr><td>Category</td>{compareList.map(p => <td key={p.product_id}>{p.category}</td>)}</tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;