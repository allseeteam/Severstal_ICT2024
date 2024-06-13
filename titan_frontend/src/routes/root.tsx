import { Route, Routes } from 'react-router-dom';
import Layout from '../components/layout';
import { AuthProvider, RequireAuth } from '../components/auth-provider';
import ReportsPage from './reports/reports';
import LoginPage from './login/login';
import { ErrorPage, RootBoundary } from '../error-page';
import ReportsCreatePage from './reports/reports-create';
import SupportPage from './support/support';
import ReportPreviewPage from './reports/report-preview';
import PreferencesPage from './user/preferences';

export default function Root() {
  return (
    <div>
      <AuthProvider>
        <Routes>
          <Route element={<Layout />} errorElement={<RootBoundary />}>
            <Route
              path="/"
              element={
                <RequireAuth>
                  <ReportsPage />
                </RequireAuth>
              }
            />
            <Route
              path="/reports/:reportId"
              element={
                <RequireAuth>
                  <ReportPreviewPage />
                </RequireAuth>
              }
            />
            <Route
              path="/reports"
              element={
                <RequireAuth>
                  <ReportsPage />
                </RequireAuth>
              }
            />
            <Route
              path="/generate"
              element={
                <RequireAuth>
                  <ReportsCreatePage />
                </RequireAuth>
              }
            />
            <Route
              path="/preferences"
              element={
                <RequireAuth>
                  <PreferencesPage />
                </RequireAuth>
              }
            />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/support" element={<SupportPage />} />
            <Route path="*" element={<ErrorPage />} />
          </Route>
        </Routes>
      </AuthProvider>
    </div>
  );
}
