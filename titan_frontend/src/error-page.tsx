import { Link, isRouteErrorResponse, useRouteError } from 'react-router-dom';

export function RootBoundary() {
  const error = useRouteError();
  console.error(error);

  if (isRouteErrorResponse(error)) {
    if (error.status === 404) {
      return <div>This page doesn't exist!</div>;
    }

    if (error.status === 401) {
      return <div>You aren't authorized to see this</div>;
    }

    if (error.status === 503) {
      return <div>Looks like our API is down</div>;
    }

    if (error.status === 418) {
      return <div>🫖</div>;
    }
  }

  return <div>Something went wrong</div>;
}

export function ErrorPage() {
  return (
    <div id="error-page">
      <h1>Упс!</h1>
      <p>Возникла неожиданная ошибка.</p>
      <Link to="/" className="hover:underline text-blue-d2">
        На главную страницу
      </Link>
    </div>
  );
}
