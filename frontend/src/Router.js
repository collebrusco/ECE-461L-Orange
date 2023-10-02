import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
  Navigate,
} from "react-router-dom";
import UserManagement from "./pages/UserManagement";
import ResourceManagement from "./pages/ResourceManagement";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route index path="user" element={<UserManagement />} />
      <Route path="resource" element={<ResourceManagement />} />
      <Route path="*" element={<Navigate to="user" replace />} />
    </Route>
  )
);

function Router() {
  return <RouterProvider router={router} />;
}

export default Router;
