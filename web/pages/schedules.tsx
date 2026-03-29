import Layout from '../components/Layout';

export default function Schedules() {
  return (
    <Layout>
      <h2>Schedules</h2>
      <div className="card">
        <p>Manage weekly schedules and apply quick shortcuts.</p>
        <div className="grid">
          <div className="card">
            <h4>Bulk Actions</h4>
            <button className="button">Copy Monday</button>
            <button className="button">Apply to All Weekdays</button>
          </div>
          <div className="card">
            <h4>Weekly Grid</h4>
            <p>Mon-Fri 09:00 - 17:00</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
