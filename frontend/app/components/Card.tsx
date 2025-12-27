type CardProps = {
  title: string;
  children?: React.ReactNode;
};

export default function Card({ title, children }: CardProps) {
  return (
    <section
      style={{
        border: "1px solid #e5e5e5",
        borderRadius: "12px",
        padding: "16px",
        background: "#fff",
      }}
    >
      <h2 style={{ fontSize: "16px", fontWeight: 600, marginBottom: "8px" }}>
        {title}
      </h2>

      <div style={{ color: "#555", fontSize: "14px" }}>
        {children || "Card content will appear here."}
      </div>
    </section>
  );
}