interface Props {
  items: string[];
}

export default function PackingCard({ items }: Props) {
  return (
    <section style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
      <h3>Spakiraj</h3>
      {items.length === 0 ? (
        <p>Nema posebnih preporuka za pakiranje - osim dobre volje!</p>
      ) : (
        <ul style={{ listStyleType: "disc", paddingLeft: 16 }}>
          {items.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
