import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LLMs 101 Workbench",
  description: "Local LLM systems workbench"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
