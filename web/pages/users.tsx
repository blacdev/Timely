import Layout from '../components/Layout';

export default function Users() {
  return (
    <Layout>
      <h2>Users & Roles</h2>
      <div className="card">
        <button className="button">Invite User</button>
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Super Admin</td>
              <td>admin@example.com</td>
              <td>Super Admin</td>
              <td>Active</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
