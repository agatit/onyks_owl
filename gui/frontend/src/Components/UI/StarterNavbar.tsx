import { Navbar, Container } from "react-bootstrap";

function StarterNavbar() {
  return (
    <Navbar bg="dark" variant="light">
      <Container>
        <Navbar.Brand href="#home">
          <img
            src="/logo.png"
            width="100"
            height="30"
            className="d-inline-block align-top"
            alt="React Bootstrap logo"
          />
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default StarterNavbar;
