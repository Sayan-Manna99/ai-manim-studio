"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [backendStatus, setBackendStatus] = useState("Checking...");

  useEffect(() => {
    fetch("http://localhost:8000/health")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend request failed");
        }

        return response.json();
      })
      .then((data) => {
        setBackendStatus(data.status);
      })
      .catch(() => {
        setBackendStatus("Backend unavailable");
      });
  }, []);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-3xl font-bold">AI Manim Studio</h1>

        <p className="mt-4">
          Backend status: <span className="font-semibold">{backendStatus}</span>
        </p>
      </div>
    </main>
  );
}
