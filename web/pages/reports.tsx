import Layout from '../components/Layout';

export default function Reports() {
  return (
    <Layout>
      <h2>Reports</h2>
      <div className="card">
        <button className="button">Generate Monthly Report</button>
        <p>Download monthly Excel workbooks and individual user reports.</p>
      </div>
    </Layout>
  );
}
