"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <main id="main-content" className="shell-page" role="alert">
      <h1>Something went wrong</h1>
      <p>An unexpected error occurred in the application shell.</p>
      <button type="button" onClick={() => reset()}>
        Try again
      </button>
    </main>
  );
}
