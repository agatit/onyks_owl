import { Container } from "react-bootstrap";

function StarterFooter(props: any) {
  return (
    <div style={footerStyle}>
      <Container fluid>{props.children}</Container>
    </div>
  );
}

export default StarterFooter;

const footerStyle = {
  background: "rgb(150,150,150)",
  padding: "2em",
};
