// index.js
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { AuthProvider } from "react-oidc-context";

const cognitoAuthConfig = {
  authority:
    "https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_3jHoa6lMn",
  client_id: "2uiog0l5j4v9flu4ifk5efea2n",
  redirect_uri: "https://d84l1y8p4kdic.cloudfront.net",
  response_type: "code",
  scope: "email openid phone",
};

const root = ReactDOM.createRoot(document.getElementById("root"));

// wrap the application with AuthProvider
root.render(
  <React.StrictMode>
    <AuthProvider {...cognitoAuthConfig}>
      <App />
    </AuthProvider>
  </React.StrictMode>,
);
