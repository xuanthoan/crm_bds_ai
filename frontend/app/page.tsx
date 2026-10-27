import Link from "next/link";

export default function HomePage() {
  return (
    <main id="main-content" className="shell-page">
      <header className="shell-header">
        <p className="eyebrow">Sprint 1 · Engineering Foundation</p>
        <h1>CRM_BDS_AI Frontend Shell</h1>
      </header>
      <p className="lead">
        This is the application shell only. No business screens are implemented
        in Sprint 1 (see the Sprint 1 Execution Pack scope).
      </p>
      <nav aria-label="Shell routes" className="shell-nav">
        <ul>
          <li>
            <Link href="/health">Health check page</Link>
          </li>
        </ul>
      </nav>
      <footer className="shell-footer">
        <span role="status">API contract: OpenAPI 3.1 (generated, do not edit manually)</span>
      </footer>
    </main>
  );
}
