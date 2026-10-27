import Link from "next/link";

export default function NotFound() {
  return (
    <main id="main-content" className="shell-page">
      <h1>404 — Page not found</h1>
      <p>The requested page does not exist in this shell.</p>
      <Link href="/">Back to the shell home</Link>
    </main>
  );
}
