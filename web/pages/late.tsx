import Layout from '../components/Layout';

export default function Late() {
  return (
    <Layout>
      <h2>Late Requests</h2>
      <div className="card">
        <h3>Pending</h3>
        <table className="table">
          <thead>
            <tr>
              <th>User</th>
              <th>ETA</th>
              <th>Reason</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Alex</td>
              <td>09:30</td>
              <td>Traffic</td>
              <td>
                <button className="button">Approve</button>
                <button className="button">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
