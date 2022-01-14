import { Container } from "react-bootstrap";
import { Navbar } from "react-bootstrap";

function Nav(props: any) {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand href="/">Onyks_owl</Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default Nav;
