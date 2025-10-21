interface Props {
  rationale: string;
}

export default function WhyDetails({ rationale }: Props) {
  return (
    <section style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
      <details>
        <summary style={{ cursor: "pointer", fontWeight: 600 }}>Zašto ove preporuke?</summary>
        <p style={{ marginTop: 8 }}>{rationale}</p>
      </details>
    </section>
  );
}
