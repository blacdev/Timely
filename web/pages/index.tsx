import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <h2>Overview</h2>
      <div className="grid">
        <div className="card">
          <h3>Today</h3>
          <p>Clock-ins, clock-outs, and exceptions for the current day.</p>
        </div>
        <div className="card">
          <h3>Pending Late Requests</h3>
          <p>Review late requests and approve or reject them.</p>
        </div>
        <div className="card">
          <h3>Monthly Report Status</h3>
          <p>Track the latest monthly report run.</p>
        </div>
      </div>
    </Layout>
  );
}
