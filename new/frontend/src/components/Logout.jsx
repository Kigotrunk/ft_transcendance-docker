import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Logout = ({setAccessToken}) => {

	const navigate = useNavigate();

	useEffect(() => {
		setAccessToken(null);
		localStorage.removeItem('accessToken');
		navigate('/');
	});
	
	return null;
}

export default Logout;