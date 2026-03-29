import Layout from '../components/Layout';

export default function Setup() {
  return (
    <Layout>
      <h2>Setup Wizard</h2>
      <div className="card">
        <h3>Organization</h3>
        <p>Configure allowed email domain, server base URL, timezone, and rule thresholds.</p>
        <form>
          <label>
            Allowed domain
            <input type="text" placeholder="example.com" />
          </label>
          <label>
            Server Base URL
            <input type="text" placeholder="http://192.168.1.10" />
          </label>
        </form>
      </div>
      <div className="card">
        <h3>SMTP Test</h3>
        <p>Save and test SMTP settings for monthly report emails.</p>
      </div>
    </Layout>
  );
}
