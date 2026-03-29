import Link from 'next/link';
import { ReactNode } from 'react';

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>Timely Admin</h1>
        <nav>
          <Link href="/">Overview</Link>
          <Link href="/setup">Setup</Link>
          <Link href="/users">Users & Roles</Link>
          <Link href="/schedules">Schedules</Link>
          <Link href="/attendance">Attendance</Link>
          <Link href="/late">Late Requests</Link>
          <Link href="/reports">Reports</Link>
        </nav>
      </aside>
      <main className="content">{children}</main>
    </div>
  );
}
