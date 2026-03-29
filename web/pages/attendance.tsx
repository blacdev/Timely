import Layout from '../components/Layout';

export default function Attendance() {
  return (
    <Layout>
      <h2>Attendance Dashboard</h2>
      <div className="card">
        <p>Filter by date range, user, or compare overlays.</p>
        <div className="grid">
          <div className="card">Line chart placeholder</div>
          <div className="card">Bar chart placeholder</div>
          <div className="card">Heatmap placeholder</div>
          <div className="card">Scatter plot placeholder</div>
          <div className="card">Box plot placeholder</div>
          <div className="card">Stacked bar placeholder</div>
        </div>
      </div>
    </Layout>
  );
}
